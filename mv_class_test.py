import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user = ""
password = ""
yourip = ""
apiinternal = "https://"+yourip+"/api/internal/"

class ManagedVolume:
    def __init__(self, mvname):
        self.managedvolume = mvname

    def getmvid(self):
        response = requests.get(apiinternal+"managed_volume", auth=(user, password), verify=False).json()
        for i,e in enumerate(response['data']):
            if self.managedvolume == response['data'][i]['name']:
                self.mvid = response['data'][i]['id']
                print("mvid is set to: " + str(self.mvid)) 
                return

    def beginSnapshot(self):
        result = requests.post(apiinternal+"managed_volume/"+self.mvid+"/begin_snapshot", auth=(user,password), verify=False)
        return result.json()

    def endSnapshot(self):
        result = requests.post(apiinternal+"managed_volume/"+self.mvid+"/end_snapshot", auth=(user,password), verify=False)
        return result.json()

    def getSnapshots(self):
        result = requests.get(apiinternal+"managed_volume/"+self.mvid+"/snapshot", auth=(user,password), verify=False)
        result = result.json()
        self.snapshots = result['data']
        return
        
    def getSnapId(self,date):
        snapshotlist = []
        choices = {}
        self.getSnapshots()
        for r,e in enumerate(self.snapshots):
            if date == str(self.snapshots[r]['date'])[:10]:
                snapshotlist.append({self.snapshots[r]['id'] : self.snapshots[r]['date']})
        
        for snap,e in enumerate(snapshotlist):
            print ('['+str(snap)+']'+" : "+ str(snapshotlist[snap]))
            choices['snap'+str(snap)] = snapshotlist[snap]
        
        x = str(input("Choose snapshot number: "))
        snapshot = choices['snap'+str(x)]
        self.snapid = list(snapshot.keys())[0]
        return list(snapshot.keys())[0]
        
    def exportSnapToHost(self):
        hostip = input("Input IP you wish to export snapshot to: ")
        data = '{ "hostPatterns": ['+'"'+hostip+'"'+'], "shareType" : "NFS"}' 
        result = requests.post(apiinternal+'managed_volume/snapshot/'+self.snapid+'/export', auth=(user,password), data=data, verify=False).json()
        time.sleep(10)
        updstatus = requests.get(result['links'][0]['href'], auth=(user,password), verify=False).json()
        channel = requests.get(updstatus['links'][0]['href'], auth=(user, password), verify=False).json()
        return channel['channels']
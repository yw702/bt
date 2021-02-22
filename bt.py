BATTERY_LEVEL_MIN = 30
BATTERY_LEVEL_MAX = 100
SPOT_TOTAL = 20
DUSTY_TOTAL = 35

class vacuum:

    def __init__(self, data):
        self.blackboard = data
        self.total_time = 0
        self.spot_time = 0
        self.dusty_time = 0 

    #find path to charging base
    def find_home(self):
        print("Find Home - RUNNING")
        print("Find Home - SUCCEEDED; Go " + self.blackboard["HOME_PATH"])
        return self.blackboard["HOME_PATH"]
    
    #back to charging base
    def go_home(self, path):
        print("Go Home - RUNNING")
        print("Go Home - SUCCEEDED")   

    #docking procedure
    def dock(self):
        while self.blackboard["BATTERY_LEVEL"] < BATTERY_LEVEL_MAX:
            self.blackboard["BATTERY_LEVEL"] += 1
            print("Dock - RUNNING; Battery Level=" + str(self.blackboard["BATTERY_LEVEL"]) + "%")
        print("Dock - SUCCEEDED")  

    #general cleaning start
    def clean(self):
        print("General Cleaning - RUNNING")   

    #general cleaning finished
    def done_general(self):
        self.blackboard["GENERAL"] = False
        print("General Cleaning - SUCCEEDED")

    #spot cleaning
    def clean_spot(self):
        print("Spot Cleaning - RUNNING")

    #spot cleaning finished
    def done_spot(self):
        self.blackboard["SPOT"] = False
        print("Spot Cleaning - SUCCEEDED")

    #dusty spot finished
    def done_dusty_spot(self):
        self.blackboard["DUSTY_SPOT"] = False
        print("Dusty Spot Cleaning - SUCCEEDED")

    #dusty spot fail
    def fail_dusty_spot(self):
        print("Dusty Spot Cleaning - FAILED")
        self.blackboard["DUSTY_SPOT"] = False
    
    def p1(self):
        if self.blackboard["BATTERY_LEVEL"] < BATTERY_LEVEL_MIN:
            if self.blackboard["GENERAL"] and self.total_time > 0:
                self.done_general()
                if self.blackboard["DUSTY_SPOT"]:
                    self.fail_dusty_spot()
            self.go_home(self.find_home())
            self.dock()  

    def p2(self):
        # Spot Clean
        if self.blackboard["SPOT"]:
            if self.spot_time < SPOT_TOTAL:
                self.clean_spot()
                self.spot_time += 1
            else:
                self.done_spot()

        # General clean
        if self.blackboard["GENERAL"]:
            if self.blackboard["BATTERY_LEVEL"] >= BATTERY_LEVEL_MIN:
                if self.blackboard["DUSTY_SPOT"]:
                    if self.dusty_time < DUSTY_TOTAL:
                        self.clean_spot()
                        self.dusty_time += 1
                    else:
                        self.done_dusty_spot()
                self.clean()
            else:
                print("General Cleaning - FAILED")
        elif self.blackboard["DUSTY_SPOT"]:
            self.fail_dusty_spot()

    def p3(self):
        print("Do Nothing")

    def check_progress(self):
        return self.blackboard["SPOT"] or self.blackboard["GENERAL"] or self.blackboard["DUSTY_SPOT"]
  
    def run(self):
        while self.check_progress():
            self.p1()
            self.p2()
            self.p3()
            self.total_time += 1
            self.blackboard["BATTERY_LEVEL"] -= 1     


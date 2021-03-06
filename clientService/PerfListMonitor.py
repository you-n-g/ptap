
from Monitor import *
import shutil
from PerfListMetricsManager import *

class PerfListConfig(MonitorConfig):
    def __init__(self):
        super(PerfListConfig, self).__init__()
	self.rPath = ''
	self.file_name = 'report.dat'

    def getOutputPath(self):
	temp = self.root_path + '/AllSource/ClientOutput/' + self.rPath + '/Raw/Events/Perf/'
	try:
		shutil.rmtree(temp)
	except:
		pass
	if not os.path.exists(temp):
		os.makedirs(temp)
	return temp + self.file_name

class PerfListMonitor(Monitor):
	#testCommand = 'sudo perf stat -o %s -e %s %s'
	#testPidCommand = 'sudo perf stat -o %s -e %s -p %s sleep %s'
	testPlatformCommand = 'sudo perf stat -o %s -a -e %s sleep %s'

	def __init__(self, metricsManager=PerfListMetricsManager(PerfListMetricsManagerConfig()), config=PerfListConfig()):
		Monitor.__init__(self, config)
		self.metrics_manager = metricsManager

	def monitoringPlatform(self, rPath, duration, delay):
		self.config.rPath = rPath
		outputPath = self.config.getOutputPath()
		args = [outputPath]
		events = self.metrics_manager.getAllEvents()
		args.append(events)
		args.append(duration)
		mCommand = self.testPlatformCommand % tuple(args)
		time.sleep(delay)
		out = subprocess.call(mCommand, shell=True)
	
	def run(self, job):
		rPath = job.path
		duration = job.perf_list_paras['duration']
		delay = job.perf_list_paras['delay']
		self.monitoringPlatform(rPath, duration, delay)


def main():
        from tmp import Job
        rPath = '/project1/sourcecode1/source/1/test1'
        job = Job(path=rPath, pid='-1', sar_paras={'interval':0,'loops':0}, pmu_paras={}, hotspots_paras={'duration':5}, perf_list_paras={'duration': 10, 'delay': 0})
        monitor = PerfListMonitor()
        monitor.run(job)

if __name__ == '__main__':
        main()

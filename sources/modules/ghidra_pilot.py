import os, subprocess, threading, time, readline

def get_ghidra_headless_path():
	ghidra_headless = os.environ.get('GHIDRA_HEADLESS_PATH')
	if ghidra_headless:
		return ghidra_headless
	else:
		ghidra_headless = input("Please enter the path to Ghidra Headless folder: ")
		# Save the PATH permanently in the system
		with open(os.path.expanduser("~/.bashrc"), "a") as f:
			f.write(f'\nexport GHIDRA_HEADLESS_PATH="{ghidra_headless}"')
		os.environ['GHIDRA_HEADLESS_PATH'] = ghidra_headless
		return ghidra_headless

# Setting path
ghidra_path = get_ghidra_headless_path()

def exec_headless(file, script):
	"""
	Execute the headless analysis of ghidra
	"""
	path = ghidra_path + 'analyzeHeadless'
	# Setting variables
	tmp_folder = "/tmp/out"
	os.mkdir(tmp_folder)
	cmd = ' ' + tmp_folder + ' TMP_DIR -import'+ ' '+ file + ' '+ "-postscript "+ script +" -deleteProject"	

	# Running ghidra with specified file and script
	try:	
		#os.system(cmd)
		p = subprocess.run([str(path + cmd)], shell=True, capture_output=True)
		os.rmdir(tmp_folder)

	except KeyError as e:
		print(e)
		os.rmdir(tmp_folder)


def decompiling(file):
	"""
	Execute the decompiling script
	"""

	# Setting script
	script = "modules/scripts/ghidra_decompiler.py"

	# Start the exec_headless function in a new thread
	thread = threading.Thread(target=exec_headless, args=(file, script))
	thread.start()

	# Animate the loading while waiting for the thread to finish
	animation = "|/-\\"
	idx = 0
	while thread.is_alive():
		print("Decompiling your binary... " + animation[idx % len(animation)], end="\r")
		idx += 1
		time.sleep(0.1)
	print("Binary successfully decompiled !")

def vuln_hunting(file):
	"""
	Execute the vulnerability hunting script
	"""

	# Setting script
	script = "modules/scripts/vuln_hunting.py"
	
	# Start the exec_headless function in a new thread
	thread = threading.Thread(target=exec_headless, args=(file, script))
	thread.start()

	# Animate the loading while waiting for the thread to finish
	animation = "|/-\\"
	idx = 0
	while thread.is_alive():
		print("Performing a vulnerability analysis... " + animation[idx % len(animation)], end="\r")
		idx += 1
		time.sleep(0.1)
	print("File successfully analysed !")
import os

def merge_dicts(arr):
	res = {}
	for a in arr:
		res.update(a)
	return res

def write_binary_file(path, content):
	with open(path, 'wb') as f:
		f.write(content)

def read_text_file(path):
	with open(path, 'rb') as f:
		return f.read().decode('utf-8')
	return None

def read_binary_file(path):
	with open(path, 'rb') as f:
		return f.read()
	return None

def ensure_folder(path):
	if not os.path.exists(path):
		os.makedirs(path)

def to_bytes(text):
	return bytes(text, 'utf-8')

def allfiles(root, postfix = ''):
	files = []
	full_root = os.path.join(root, postfix)
	for name in os.listdir(full_root):
		local_name = os.path.join(postfix, name)
		full_name = os.path.join(root, postfix, name)
		if os.path.isdir(full_name):
			files += allfiles(root, local_name)
		elif os.path.isfile(full_name):
			files.append(local_name)
	return files
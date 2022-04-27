1. Link of Video: (maybe you need to download video from google drive by this link)

	https://drive.google.com/file/d/1n46Ko1zqkbgcX8h4bg6P1hnfSEaJc147/view?usp=sharing
	
	
2. Link to my web service: http://168.138.13.227:31000/ 

	- To send request, please use the following command:
	(you may need to change command "python" to "python3")
	(the last number -- "1", is the number of thread)

	python iWebLens_client.py inputfolder/ http://168.138.13.227:31000/api/object_detection 1

3. ZIP file
	- dockerfile, deployment.yml, service.yml and all web service source code files are in the "webservice_file" folder

	- I split server side as two python files. run "iWebLens_server.py" and it will call a function in "object_detection_modified.py"
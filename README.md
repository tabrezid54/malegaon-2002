# Driver Assistant Application

DA - Driver Assistant Application is one of the two primary components of OCS(On-board Computing System). 
This application runs on the device called OBU(on-board Unit) which will be in the WM truck. This application allows the driver to capture all route information electronically.

This is a natvie android application which communicates with the below applications/services. 

1. Driver Security Service - for logging
2. OCS - to get/send all the route information
3. DADispatcher - to push Driver Idles
4. AWS-S3 - to upload snapshot/disposal images  
    - Landfill Images gets uploaded to the WM App Engineering Account in respective Bucket name mentioned in TP_SYSTEMPARAMETER 
    - Container Repair Images gets uploaded to the  Account in respective Bucket name mentioned in TP_SYSTEMPARAMETER  
    - Rest All images are getting uploaded to the below AWS Account in respective Bucket and Folder names mentioned in TP_SYSTEMPARAMETER
        - Account: 991043543243
        - AWS_OpsProd_ReadOnly 
5. AWS-dynamodb - to upload safetyform data
    - ETA data is uplaoded to the Dynamo DB to the below AWS Account 
	- Same is maintained for DA Configuration
        - Account: 535855658044
        - AWS_OCS


# Android Version Targetting
DA is currently built to work with Android API 23(MARSHMALLOW). However, DA's minimun SDK support is 23(MARSHMALLOW). SQLite is the database engine for this application.

#Build Configuraton
This project was build on JDK1.7. This project uses ANT as the build and dependency management system. Patch files are used to change the environment based properties in app.xml & config.xml files at teh time of build. 

### Change Log
For details on per release changes please review [CHANGELOG](https://github.wm.com/operations/DriverApplication/blob/master/CHANGELOG.md/).
# malegaon-2002

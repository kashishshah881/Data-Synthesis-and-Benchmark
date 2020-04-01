# Data Synthesis and Benchmark

In this project we will develop a data pipeline to train and benchmark multiple Synthetic data
generators and then deploy them in production on the cloud. The need to synthesis data (or generate synthetic data) are in the following scenario: <br>
1. Extracting Data is Expensive. Example: Oil Fields,Mining etc <br>
2. The data doesnt exist. 
3. Some data is confidential and thus not completely available. Example: Banking data

## Flowchart

<img src="https://github.com/kashishshah881/datasynthesis/blob/master/data/flow.png" width="480">

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
Python 3.7+
AWS Account
GCP Account
Docker
```

### Installing

```
pip3 install -r requirements.txt
```
### Steps

##### Step 1:
- Create a AWS Account. Get Started [Here](aws.amazon.com)
- Configure IAM Role having Full S3 Bucket Access in your local environment. Learn More [Here](https://docs.databricks.com/administration-guide/cloud-configurations/aws/iam-roles.html#step-1-create-an-iam-role-and-policy-to-access-an-s3-bucket)
- Create a GCP Account and enable API. Get Started [Here](cloud.google.com)

##### Step 2:
- Run on CLI ```aws configure```
- Configure your AWS Keys in [synthesizerfile.py](https://github.com/kashishshah881/datasynthesis/blob/master/synthesizerfile.py#L43-#L44) 
- Configure your AWS S3 Bucket in [streamlit.py](https://github.com/kashishshah881/datasynthesis/blob/master/streamlit.py#L21), [data.py](https://github.com/kashishshah881/datasynthesis/blob/master/data.py#L10) and [synthesizerfile.py](https://github.com/kashishshah881/datasynthesis/blob/master/synthesizerfile.py#L37)
  
#### Step 3:
- Run ```docker build .```

#### Step 4:
Push your docker container to your repository
- Run ```docker login --username=yourhubusername --email=youremail@company.com ```
- Run ``` docker images ```
- Run ```docker tag <Image ID> yourhubusername/projectname:<tagname> ```
- Run ``` docker push yourhubusername/verse_gapminder ```

#### Step 5:
Deploying your application on kubernetes engine
- Setup your Kubernetes Cluster.Learn more [Here](https://medium.com/platformer-blog/creating-a-kubernetes-cluster-with-google-kubernetes-engine-gke-under-5-minutes-5f5a061b3f1d)
- Open Gcloud Shell and Run:
  - Pull the image from the Repository and create a Container on the Cluster <br> ``` kubectl run my-app --image=yourhubusername/projectname:<tagname> --port=5000 deployment "my-app" created ```
  -  Getting pods info <br> ``` kubectl get pods ```
  
  - Expose the Kubernetes Deployment through a Load Balancer <br> ``` kubectl expose deployment my-app --type=LoadBalancer --port=8080 --target-port=5000 ```
  
  - Find the external IP of your Container <br> ```kubectl get svc ```
  
#### Step 6:
 You are almost done. Copy the External IP Address from Step 5 and paste it in [streamlit.py](https://github.com/kashishshah881/datasynthesis/blob/master/streamlit.py#L152)
 
 Run on CLI  ```streamlit run streamlit.py ``` <br> 
 Voila!


## Built With
* [SDGym](https://github.com/sdv-dev/SDGym) - Synthetic Data Generation Library
* [Streamlit.io](https://streamlit.io/) - Frontend Web Framework 
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Backend Web Framework
* [Dask](https:/dask.org) - Parallelizing Data generation
* [Docker](https://docker.com) - Container Framework

## Authors

* **Kashish Shah** - *Design, Architect and Deployment* - [Linkedin](https://linkedin.com/in/shah-kashish)
* **Manogana Mantripragada** - *Machine Learning Engineer* - [Linkedin](https://www.linkedin.com/in/manogna-mantripragada/)
* **Dhruv Panchal** - *Architect and Deployment* - [Linkedin](https://www.linkedin.com/in/panchaldhruv/)



## License

This project is licensed under the Commons Clause License - see the [LICENSE.md](https://commonsclause.com) file for details


## Acknowledgments

* [Kubernetes Deployment](https://codeburst.io/getting-started-with-kubernetes-deploy-a-docker-container-with-kubernetes-in-5-minutes-eb4be0e96370)

# devopsk8sHelm

K8S Helming...

Get helm at:
https://github.com/helm/helm/releases 



# add “stable” repository
$ helm repo add stable https://charts.helm.sh/stable

# sync all helm charts info.
$ helm repo update 

# By default helm uses stable repo, we can see which repos are available using list.
$ helm repo list 

# show you a list of all deployed releases.
$ helm list 

-----------------------------------------------

# add bitnami repo as a chart repository:
$ helm repo add bitnami https://charts.bitnami.com/bitnami

# Get Apache chart:
$ helm install my-release bitnami/apache

# Get our server IP address using:
$ minikube service my-release-apache --url

# Clean up
$ helm delete my-release

-----------------------------------------------
#FOR NEW CHART

# Create a chart
$ helm create mychart

# dry run
$ helm install mychart --dry-run --debug mychart

# package a chart
$ helm package mychart

# Upgrade a chart
$ helm upgrade --install mychart mychart-0.1.0.tgz --set replicaCount=3

--------------------------------------------------

# Install chart
From ~/python-rest-chart
Run: helm install primary-db ./charts/primary-db

From ~/python-rest-chart
Run: helm install python-app ./charts/python-app


# Uninstall chart
From ~/python-rest-chart
Run: helm uninstall primary-db ./charts/primary-db

From ~/python-rest-chart
Run: helm uninstall python-app ./charts/python-app


# Install Chart using Parent Chart
From ~/devops-k8s-helm
run: helm install python-rest-chart ./python-rest-chart 


MYSQL_ROOT_PASSWORD required by Mysql

+ minikube service devops-k8s-helm-service --url
! Because you are using a Docker driver on darwin, the terminal needs to be open to run it.



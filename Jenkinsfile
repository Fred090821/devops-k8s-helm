pipeline {
    agent any
   options{
        buildDiscarder(logRotator(numToKeepStr:'5', daysToKeepStr:'5'))
   }

    environment{
       HUB_REGISTRY_ID = 'adedo2009'
       APP_IMAGE_NAME = 'devops-k8s-helm'
       TEST_IMAGE_NAME = 'devops-k8s-helm-test'
       DOCKERHUB_CREDENTIALS = credentials('docker-hub')
       COMPOSE_YML_PATH = '/Users/jaydenassi/.jenkins/workspace/devops-k8s-helm'
       dockerImage = ''
   }

    stages {
        stage(' Helm Uninstall start fresh') {
            steps {
               echo ' Helm Uninstall start fresh ===> '
               script {
                    try{
                       sh '''
                          helm uninstall primary-db
                          helm uninstall python-app

                          # Check if the image exists and remove it
                          if docker images -q $APP_IMAGE_NAME 2> /dev/null; then
                              docker rmi $APP_IMAGE_NAME
                          fi

                          # Check if the image with the registry exists and remove it
                          if docker images -q $HUB_REGISTRY_ID/$APP_IMAGE_NAME 2> /dev/null; then
                              docker rmi $HUB_REGISTRY_ID/$APP_IMAGE_NAME
                          fi

                          # Check if the tagged image exists and remove it
                          if docker images -q $HUB_REGISTRY_ID/$APP_IMAGE_NAME:$BUILD_NUMBER 2> /dev/null; then
                              docker rmi $HUB_REGISTRY_ID/$APP_IMAGE_NAME:$BUILD_NUMBER
                          fi'''

                          def currentDirectory = pwd()
                          echo "CURRENT DIRECTORY: ${currentDirectory}"
                    }catch(Exception e){
                        echo 'Exception Helm Install'
                    }
                }
            }
        }
        stage(' Verify Tooling ') {
            steps {
            echo '=== Verify Tooling ==='
                script {
                    try{
                        sh '''
                              docker version
                              docker info
                              python3 --version
                            '''
                    }catch(Exception e){
                        echo 'Exception Running Back End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }
         stage(' Checkout ') {
            steps {
                echo '=== Checkout Devops Code ==='
                script {
                    // Clean the workspace
                    cleanWs()
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                    checkout([$class: 'GitSCM', branches: [[name: 'development']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/Fred090821/devops-k8s-helm.git']]])
                }
            }
        }
        stage(' Docker Build Rest Image ') {
            steps {
                script {
                    try{
                            sh 'docker build -t $APP_IMAGE_NAME ./python'
                            sh 'docker build -t $TEST_IMAGE_NAME ./python'

                    }catch(Exception e){
                        echo 'Exception Running Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage(' Log In To Docker hub ') {
            steps {
            echo '=== Log In To Docker hub ==='
                script {
                    try{
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    }catch(Exception e){
                        echo 'Exception Login into Ducker Hub'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Tag & Push Rest Image ') {
            steps {
            echo '=== Tag & Push Rest Image ==='
                script {
                    try{
                            sh '''
                              docker tag $APP_IMAGE_NAME $HUB_REGISTRY_ID/$APP_IMAGE_NAME:latest
                              docker tag $APP_IMAGE_NAME $HUB_REGISTRY_ID/$APP_IMAGE_NAME:${BUILD_NUMBER}
                              docker push -a $HUB_REGISTRY_ID/$APP_IMAGE_NAME

                              docker tag $TEST_IMAGE_NAME $HUB_REGISTRY_ID/$TEST_IMAGE_NAME:latest
                              docker tag $TEST_IMAGE_NAME $HUB_REGISTRY_ID/$TEST_IMAGE_NAME:${BUILD_NUMBER}
                              docker push -a $HUB_REGISTRY_ID/$TEST_IMAGE_NAME
                            '''
                    }catch(Exception e){
                        echo 'Exception Pushing Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage(' Helm Install Mysql') {
            steps {
               echo ' Helm Install Mysql ===> '
               script {
                    try{
                       sh '''
                        helm install primary-db ./python-rest-chart/charts/primary-db'''
                    }catch(Exception e){
                        echo 'Exception Helm Install Mysql'
                        error('Aborting the build')
                    }
                }
            }
        }
         stage(' Helm Install python-app') {
            steps {
               echo ' Helm Install python-app ===> '
               script {
                    try{
                        sh '''
                                helm install python-app ./python-rest-chart/charts/python-app --set image.python.tag="${BUILD_NUMBER}"'''

                    }catch(Exception e){
                        echo 'Exception Helm Install'
                        error('Aborting the build')
                    }
                }
            }
        }
//         stage('Parallel Stage') {
//             parallel {
//                 stage('Set the url to k8s_url') {
//                     steps {
//                        echo ' minikube service ===> '
//                        script {
//                             try{
//                                 sh '''
//                                    sleep 30
//                                    minikube service devops-k8s-helm-service --url > k8s_url.txt'''
//                                 sh '''
//                                    echo "RUNNING RUNNING" '''
//                             }catch(Exception e){
//                                 echo 'Exception Docker Rest Tests'
//                                 echo 'Exception k8s_url.txt'
//                                 error('Aborting the build')
//                             }
//                         }
//                     }
//                 }
//                 stage('Retrieve the url from k8s_url') {
//                     steps {
//                        echo ' k8s_url ===> '
//                        script {
//                             try{
//                                 sh '''
//                                     sleep 5
//                                     k8s_url = $(cat ./k8s_url.txt)
//                                     echo "CURRENT TEST URL: ${k8s_url}"
//                                     k8s_url=$(cat k8s_url.txt)'''
//                                     echo 'CURRENT TEST URL: ${k8s_url}'
//                             }catch(Exception e){
//                                 echo 'Exception Docker Rest Tests'
//                                 echo 'Exception k8s_url.txt'
//                                 error('Aborting the build')
//                             }
//                         }
//                     }
//                 }
//             }
//         }
//         stage(' Kubernetes run test ') {
//             steps {
//             echo '=== Kubernetes run test ==='
//                 script {
//                     try{
//                         if (checkOs() == 'Windows') {
//                             bat '/usr/local/bin/pytest ./pythonk8stest/pythonk8stest.py'
//                         } else {
//                             sh '/usr/local/bin/pytest ./pythonk8stest/pythonk8stest.py'
//                         }
//                     }catch(Exception e){
//                         echo 'Exception Kubernetes run test'
//                         error('Aborting The Build')
//                     }
//                 }
//             }
//         }
    }
    post {
//          always {
//         echo '=== post Clean Environment ==='
//             script {
//                 try{
//                          sh '''
//                           helm uninstall primary-db
//                           helm uninstall python-app
//
//                           # Check if the image exists and remove it
//                           if docker images -q $APP_IMAGE_NAME 2> /dev/null; then
//                               docker rmi $APP_IMAGE_NAME
//                           fi
//
//                           # Check if the image with the registry exists and remove it
//                           if docker images -q $HUB_REGISTRY_ID/$APP_IMAGE_NAME 2> /dev/null; then
//                               docker rmi $HUB_REGISTRY_ID/$APP_IMAGE_NAME
//                           fi
//
//                           # Check if the tagged image exists and remove it
//                           if docker images -q $HUB_REGISTRY_ID/$APP_IMAGE_NAME:$BUILD_NUMBER 2> /dev/null; then
//                               docker rmi $HUB_REGISTRY_ID/$APP_IMAGE_NAME:$BUILD_NUMBER
//                           fi'''
//
//                           def currentDirectory = pwd()
//                           echo "CURRENT DIRECTORY: ${currentDirectory}"
//                         // Clean the workspace
//                         // cleanWs()
//
//                 }catch(Exception e){
//                         // Catch any exception and print details
//                         echo "Exception post Clean Environment :::: ${e}"
//                         error('Aborting the build')
//                 }
//             }
//         }
        success {
            echo 'All test run successfully'
        }
        unstable {
            echo 'The build is unstable'
        }
        changed {
            echo 'The pipeline  state has changed'
        }
    }
}

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }
}

// Function to check if a directory exists
def fileExists(path) {
    def file = file(path)
    return file.exists() && file.isDirectory()
}


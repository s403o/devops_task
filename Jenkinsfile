pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: buildkit
spec:
  containers:
  - name: buildkit
    image: moby/buildkit:v0.9.0
    command: ["buildctl-daemonless.sh"]
    securityContext:
      privileged: true
"""
        }
    }

    environment {
        DOCKER_IMAGE = 's403o/flaskapp:latest'
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout from SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/s403o/devops_task'
            }
        }

        stage('Build & Push with BuildKit') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                }
                container('buildkit') {
                    sh '''
                    buildctl build --frontend=dockerfile.v0 --local context=. --local dockerfile=. --output type=image,name=s403o/flaskapp:latest,push=true
                    '''
                }
            }
        }
    }
}
pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-role
  restartPolicy: Never
  containers:
  - name: python
    image: artifactory.cloud.cms.gov/docker/python:3.11
    command: ['cat']
    tty: true
"""
    }
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Prepare') {
      steps {
        container('python') {
          sh '''
            set -eux
            python --version
            pip --version
            pip install -U pip
            if [ -f requirements.txt ]; then
              pip install --no-cache-dir -r requirements.txt
            else
              pip install --no-cache-dir boto3 pytest
            fi
          '''
        }
      }
    }

    stage('Test') {
      steps {
        container('python') {
          sh '''
            set -eux
            if ls tests/test_*.py 1> /dev/null 2>&1; then
              pytest --junitxml=results.xml
            else
              echo "No tests found; skipping pytest"
            fi
          '''
        }
      }
    }
  }

  post {
    always {
      container('python') {
        script {
          junit testResults: 'results.xml', allowEmptyResults: true
          archiveArtifacts artifacts: '**/results.xml', allowEmptyArchive: true
        }
      }
    }
  }
}

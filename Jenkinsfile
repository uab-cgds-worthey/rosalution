pipeline {
  agent any
  options {
    timestamps()
    ansiColor('xterm')
  }
  environment {
    GITLAB_API_TOKEN = credentials('GitLabToken')
    // BUILD_TAG = "a${GIT_COMMIT.substring(0, 6)}"
    BUILD_TAG = "prod"
  }
  stages {
    stage('Static Analysis') {
      agent {
        docker { image 'gitlab.rc.uab.edu:4567/center-for-computational-genomics-and-data-science/utility-images/static-analysis:v1.3'}
      }
      steps {
        sh '/bin/linting.sh'
      }
      post {
        success {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins_static_analysis"'
        }
        failure {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins_static_analysis"'
        }
      }
    }
    stage('Unit Test') {
      agent {
        docker { image 'gitlab.rc.uab.edu:4567/center-for-computational-genomics-and-data-science/utility-images/unit-test:v0.4'}
      }
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'cd frontend && yarn install'
          sh 'cd frontend && yarn test:coverage'
          sh 'cd backend && pip install -r requirements.txt --user'
          sh 'cd backend && pytest --cov=src --cov-fail-under=80 --cov-branch --cov-report=term tests/'
        }
      }
      post {
        success {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins_unit_tests"'
        }
        failure {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins_unit_tests"'
        }
      }
    }
    stage('Integration Test') {
      agent {
        docker { image 'gitlab.rc.uab.edu:4567/center-for-computational-genomics-and-data-science/utility-images/unit-test-python:v0.4'}
      }
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'cd backend && pip3 install -r requirements.txt --user'
          sh 'cd backend && pytest -s tests/integration'
        }
      }
      post {
        success {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins_unit_tests"'
        }
        failure {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins_unit_tests"'
        }
      }
    }
    stage('Compile & Publish'){
      steps {
        sh 'bash build.sh --tag ${BUILD_TAG} --push'
      }
      post {
        success {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins_unit_tests"'
        }
        failure {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins_unit_tests"'
        }
      }
    }
    stage('swarm deploy') {
      when { 
        branch 'main'
      }
      steps {
        sh 'docker stack deploy --prune --with-registry-auth --compose-file docker-compose.production.yml divergen-prod'
      }
      post {
        success {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins_unit_tests"'
        }
        failure {
          sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins_unit_tests"'
        }
      }
    }
  }
  post {
	success {
      sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=success&name=jenkins"'
    }
	failure {
      sh 'curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" "https://gitlab.rc.uab.edu/api/v4/projects/2491/statuses/${GIT_COMMIT}?state=failed&name=jenkins"'
  	}
  }
}

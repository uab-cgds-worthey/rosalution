pipeline {
  agent any
  options {
    timestamps()
    ansiColor('xterm')
  }
  environment {
    GITLAB_API_TOKEN = credentials('GitLabToken')
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
        sh 'cd frontend && yarn install'
        sh 'cd frontend && yarn test:coverage'
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


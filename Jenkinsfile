def sendEmail(message) {
    emailext body: 'Project built and deployed successfully.',
        subject: 'Atha.Yoga: CI/CD',
        from: 'Jenkins (Atha.Yoga Master Node)',
        to: '${DEFAULT_RECIPIENTS}'
}

pipeline {
    agent any
    stages {
        stage('Build') {
            environment {
                BRANCH_NAME="${env.BRANCH_NAME}"
                MASTER_ENV_LINK=credentials('MASTER_ENV_LINK')
                DEVELOP_ENV_LINK=credentials('DEVELOP_ENV_LINK')
                STAGE_ENV_LINK=credentials('STAGE_ENV_LINK')
            }
            steps {
                step([$class: 'GitHubCommitStatusSetter', statusResultSource : [$class: 'DefaultStatusResultSource']])
                sh '''
                    wget -O backend/.env.master $MASTER_ENV_LINK
                    chmod g+w backend/.env.master
                    wget -O backend/.env.develop $DEVELOP_ENV_LINK
                    chmod g+w backend/.env.develop
                    wget -O backend/.env.stage $STAGE_ENV_LINK
                    chmod g+w backend/.env.stage
                    cp backend/.env.$BRANCH_NAME backend/.env
                    docker-compose --env-file backend/.env build
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose --env-file backend/.env up -d'
            }
        }
        stage('Test') {
            environment {
                BRANCH_NAME="develop"
            }
            steps {
                script {
                    waitUntil {
                        EXIT_CODE = """${sh(
                            script: "docker inspect -f '{{.State.ExitCode}}' cypress-${BRANCH_NAME}",
                            returnStdout: true
                        )}"""
                        STATUS = """${sh(
                            script: "docker inspect -f '{{.State.Status}}' cypress-${BRANCH_NAME}",
                            returnStdout: true
                        )}"""
                        if (STATUS == "exited\n" && EXIT_CODE == "0\n") {
                            return true;
                        } else if (STATUS == "exited\n" && !(EXIT_CODE == "0\n")) {
                            error 'Failed, exiting now...'
                        } else {
                            return false
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            sendEmail('Project built and deployed successfully.')
        }
        failure {
            sendEmail('Something went wrong.')
        }
        always {
            step([$class: 'GitHubCommitStatusSetter', statusResultSource : [$class: 'DefaultStatusResultSource']])
        }
    }
}
pipeline {
  agent {
    label 'Slave_1'
}
   stages {
      stage('Clone Sources') {
        steps {	  
          checkout scm
        } 
      }
	   
      stage('Build a docker image postgres') {
         steps {
            echo 'Build process for postgres'            
            sh '''
                docker build -t="postgres:${BUILD_NUMBER}" -f Dockefile_psql .
            '''
         }
      }
      
      
      stage('Build a docker image website') {
         steps {
            echo 'Build process for app'            
            sh '''
                docker build -t="website:${BUILD_NUMBER}" -f Dockefile_app .
            '''
         }
      }
      
      
      stage('Stop running container') {
         steps {
            echo 'Stopping containers if running'
			sh '''
				echo "Stopping running containers"
				CONTAINER=`docker ps -q`
				if [ -z "$CONTAINER" ]; then
					echo "No running containers. Nothing to stop"
				else									
					docker stop ${CONTAINER}
					docker rm ${CONTAINER}
				fi
                '''
                }
                }
      
      stage('create docker network') {
         steps {
         sh '''
         if ! docker network inspect website >/dev/null 2>&1 ; then
             docker network create website
         fi
         '''
         }
         }
         
      
      stage('Run postgres container') {
         steps {
            echo 'Run postgres container'
			sh '''
				sudo docker run --name postgres --network website -p 5432:5432 -d postgres:${BUILD_NUMBER}
			'''
         }
      }
       stage('Run website container') {
         steps {
            echo 'Run postgres container'
			sh '''
				sudo docker run --name website --network website -p 3001:3001 website:${BUILD_NUMBER}
			'''
         }
      }
      
      stage('Website'){
        steps{
          echo "Done!"
          echo "Check the URL: https://`hostname`:3001"
      }
      }
      
   }
}

include .env

BLACK        := $(shell tput -Txterm setaf 0)
RED          := $(shell tput -Txterm setaf 1)
GREEN        := $(shell tput -Txterm setaf 2)
YELLOW       := $(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
PURPLE       := $(shell tput -Txterm setaf 5)
BLUE         := $(shell tput -Txterm setaf 6)
WHITE        := $(shell tput -Txterm setaf 7)
RESET 		 := $(shell tput -Txterm sgr0)

start:
	@echo ""\
		"       d8888 8888888 88888888888                                  \n"\
		"      d88888   888       888                                      \n"\
		"     d88P888   888       888                                      \n"\
		"    d88P 888   888       888   .d88b.  88888b.   .d88b.   8888b.  \n"\
		"   d88P  888   888       888  d8P  Y8b 888 '88b d8P  Y8b     '88b \n"\
		"  d88P   888   888       888  88888888 888  888 88888888 .d888888 \n"\
		" d8888888888   888       888  Y8b.     888  888 Y8b.     888  888 \n"\
		"d88P     888 8888888     888   'Y8888  888  888  'Y8888  'Y888888 \n"
	@echo "${BLACK}:: ${RED}--- LIST OF COMMANDS ---${RESET} ${BLACK}::${RESET}\n"
	@echo "* INSTALL DEPENDENCIES:"
	@echo 'make devel'
	@echo 'make production'
	@echo ''
	@echo "* RUN PROJECT:"
	@echo 'make run'
	@echo 'make run-production'
	@echo ''
	@echo "* INSTALL DEPENDENCIES ON DIFFERENT MACHINES:"
	@echo "make production-backend"
	@echo "make production-nodered"
	@echo ''
	@echo "* RUN PROJECT ON DIFFERENT MACHINES:"
	@echo 'make run-production-backend'
	@echo 'make run-production-nodered'
	@echo ''
	@echo '* REBUILD FRONTEND FILES WITHOUT REINSTALLING THE BACKEND:'
	@echo 'rebuild-production-frontend'

devel:
	@sh scripts/config_env.sh $@ devel
	@echo "Set environment variables...${GREEN}[OK]${RESET}"
	@sudo docker-compose up -d
	@echo "${PURPLE}[LOG]${RESET} - Waiting for the containers to be ready"
	@sh scripts/wait_containers.sh
	@echo "Run containers...${GREEN}[OK]${RESET}"
	@echo "${PURPLE}[LOG]${RESET} - Running migrates"
	@sudo docker exec backend-aitenea bash -c "sh ../scripts/remove_migrates.sh"
	@sudo docker exec backend-aitenea bash -c "sh ../scripts/install_migrates.sh"
	@echo "${PURPLE}[LOG]${RESET} - Generating docs"
	@sudo docker exec backend-aitenea sh -c "cd ../docs && make html"
	@sudo docker-compose stop
	@echo ""
	@echo '${PURPLE}[LOG]${RESET} - The installation is complete. To start the project run: "make run"'

production:
	@sh scripts/config_env.sh $@ production
	@echo "Set environment variables...${GREEN}[OK]${RESET}"
	@sh scripts/install_postgresql.sh
	@sh scripts/install_backend.sh
	@echo "${PURPLE}[LOG]${RESET} - Generating docs"
	@sudo $(MAKE) -C aitenea_api/docs html
	@sh scripts/install_nodered.sh
	@echo '${PURPLE}[LOG]${RESET} - The installation is complete'

production-backend:
	@sh scripts/config_env.sh $@ production-backend
	@echo "Set environment variables...${GREEN}[OK]${RESET}"
	@sh scripts/install_postgresql.sh
	@sh scripts/install_backend.sh
	@echo '${PURPLE}[LOG]${RESET} - The installation is complete'

production-nodered:
	@echo "IPs and ports configuration..."
	@sh scripts/config_env.sh $@ production-nodered
	@echo "Set environment variables...${GREEN}[OK]${RESET}"
	@sh scripts/install_nodered.sh
	@echo '${PURPLE}[LOG]${RESET} - The installation is complete'

run:
	@sudo docker-compose up

run-production-backend:
	@sudo python3 /opt/aitenea/aitenea_api/manage.py runserver ${BACKEND_IP}:${BACKEND_PORT}

run-production-nodered:
	@node-red

rebuild-production-frontend:
	@sh scripts/rebuild-frontend
	@echo '${PURPLE}[LOG]${RESET} - Frontend updated'

generate-production-docs:
	@sudo $(MAKE) -C docs html
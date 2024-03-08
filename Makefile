# Rule to run the new container
up:
	@echo "Performing run..."
	docker compose up -d

down:
	@echo "Performing down..."
	docker compose down

logs:
	@echo "Performing logs..."
	docker compose -p devops_task logs -f

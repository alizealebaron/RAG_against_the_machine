# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : Makefile                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/02/26 12:46:41 by alebaron                                #
# @update   : 2026/06/27 13:13:39 by alebaron                                #
# ************************************************************************** #

# ============================================================================
#                                  Variables
# ============================================================================

NAME = RAG_against_the_machine
MYPY_FLAGS    = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip
SRC_UV        = src
SRC           = student/src/
UV_INSTALL    = curl -LsSf https://astral.sh/uv/install.sh | sh
UV_VERSION    = uv --version

# ============================================================================
#                                   Colors
# ============================================================================

BLACK   := \033[30m
RED     := \033[31m
GREEN   := \033[32m
YELLOW  := \033[33m
BLUE 	:= \033[96m
MAGENTA := \033[38;5;206m
CYAN    := \033[36m
WHITE   := \033[37m
RESET   := \033[0m
BOLD    := \033[1m
DIM     := \033[2m
ITALIC  := \033[3m
UNDER   := \033[4m
BLINK   := \033[5m
REVERSE := \033[7m
HIDDEN  := \033[8m
PINK 	:= \033[35m

# ============================================================================
#                               Mandatory Rules
# ============================================================================

# Install the Python packages used in RAG
install:
	@echo "$(CYAN)Installing ${NAME} packages...$(RESET)"
	@if ! $(UV_VERSION) > /dev/null 2>&1; then\
		$(UV_INSTALL); \
	fi
	@uv sync
	@echo "$(GREEN)✅ Packages installed !$(RESET)"

# Run the main file of RAG
run :
# 	@cd student && uv run python -m $(SRC_UV) search "What activation does EmbeddingPoolerHead use by default ?" 5
	@cd student && uv run python -m $(SRC_UV) index 2000

# Run the main file of RAG in debug mode
debug:
	@echo "$(YELLOW)Running in DEBUG mode$(RESET)"
	@uv run -m pdb $(SRC)

# Cleaning up all unnecessary Python files
clean :
	@echo "$(RED)$(BOLD)[Cleaning useless objects of ${NAME}]$(RESET)"
	@rm -rf .mypy_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +

# Checking flake8 and mypy norm
lint:	
	@echo "$(PINK)$(BOLD)[Checking mypy and flake8 norm]$(RESET)"
	@-uv run flake8 ${SRC} 
	@-uv run mypy ${SRC} $(MYPY_FLAGS)

# Checking flake8 and mypy norm in strict mode
lint-strict:
	@echo "$(PINK)$(BOLD)[Checking mypy and flake8 norm in strict mode]$(RESET)"
	@-uv run flake8 ${SRC}
	@-uv run mypy ${SRC} $(MYPY_FLAGS) --strict

# ============================================================================
#                            Quality of life Rules
# ============================================================================

#             HELP
# =============================

all : help

help :
	@echo ""
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║                   RAG - Makefile commands                  ║$(RESET)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "  $(PINK)make $(RESET)                   $(ITALIC)# Install dependencies$(RESET)"
	@echo "  $(PINK)make index$(RESET)              $(ITALIC)# Index the vLLM repository using BM25$(RESET)"
	@echo "  $(PINK)make search$(RESET)             $(ITALIC)# Test the retriever on a question$(RESET)"
	@echo "  $(PINK)make answer$(RESET)             $(ITALIC)# Complete RAG chain for a given question$(RESET)"
	@echo "  $(PINK)make search_dataset$(RESET)     $(ITALIC)# Search the entire dataset$(RESET)"
	@echo "  $(PINK)make answer_dataset$(RESET)     $(ITALIC)# Generates LLM responses for the dataset$(RESET)"
	@echo "  $(PINK)make evaluate$(RESET)           $(ITALIC)# Calculate Recall@k$(RESET)"
	@echo ""
	@echo "  $(GREEN)make lint$(RESET)               $(ITALIC)# Checking Flake8 + mypy norm$(RESET)"
	@echo "  $(GREEN)make clean$(RESET)              $(ITALIC)# Clears Python caches$(RESET)"
	@echo "  $(GREEN)make clean_index$(RESET)        $(ITALIC)# Deletes the BM25 index and chunk$(RESET)"
	@echo "  $(GREEN)make clean_output$(RESET)       $(ITALIC)# Deletes the output files$(RESET)"
	@echo "  $(GREEN)make fclean$(RESET)             $(ITALIC)# Clean everything$(RESET)"
	@echo ""

#             CLEAN
# =============================

# Cleaning up all unnecessary Python files
clean_index :
	@echo "$(RED)$(BOLD)[Cleaning index objects of ${NAME}]$(RESET)"
	@rm -rf data/processed

clean_output :
	@echo "$(RED)$(BOLD)[Cleaning output objects of ${NAME}]$(RESET)"
	@rm -rf data/output

fclean : clean clean_index clean_output

#              MAKE
# =============================

index : install
	@echo "$(YELLOW)Waiting for index...$(RESET)"
	@cd student && uv run python -m $(SRC_UV) index 2000

search : install
	@echo "$(YELLOW)Waiting for search...$(RESET)"
	@cd student && uv run python -m $(SRC_UV) search "What hardware platforms does vLLM support?" 4

search_dataset : install
	@echo "$(YELLOW)Waiting for search...$(RESET)"
	@cd student && uv run python -m $(SRC_UV) search_dataset --dataset_path ../data/datasets/public/UnansweredQuestions/dataset_docs_public.json --k 10 --save_directory ../data/output/search_results

# ============================================================================
#                               Usefull things
# ============================================================================

# Prevent rule to be associated with files.
.PHONY: install clean run debug lint lint-strict all help
.SILENT:
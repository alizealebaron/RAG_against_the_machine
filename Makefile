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
# @update   : 2026/05/15 10:50:51 by alebaron                                #
# ************************************************************************** #

# ==========================
#         Variables
# ==========================

NAME = RAG_against_the_machine
MYPY_FLAGS    = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip
SRC           = src
UV_INSTALL    = curl -LsSf https://astral.sh/uv/install.sh | sh
UV_VERSION    = uv --version

# ==========================
#           Colors
# ==========================

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

# ==========================
#           Rules
# ==========================

# Install the Python packages used in call_me_maybe
install:
	@echo "$(CYAN)Installing ${NAME} packages...$(RESET)"
	@if ! $(UV_VERSION) > /dev/null 2>&1; then\
		$(UV_INSTALL); \
	fi
	@uv sync
	@echo "$(GREEN)✅ Packages installed !$(RESET)"

# Run the main file of call_me_maybe
run :
	@uv run python -m $(SRC)

# Run the main file of call_me_maybe in debug mode
debug:
	@echo "$(YELLOW)Running in DEBUG mode$(RESET)"
	@uv run -m pdb src

# Cleaning up all unnecessary Python files
clean :
	@echo "$(RED)$(BOLD)[Cleaning useless objects of ${NAME}]$(RESET)"
	@rm -rf .mypy_cache
	@rm -rf data/processed
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

# Prevent rule to be associated with files.
.PHONY: install clean run debug lint lint-strict
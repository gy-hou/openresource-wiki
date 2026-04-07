.PHONY: serve build clean install lint new-post deploy help

# 默认目标
help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装依赖
	pip install -r requirements.txt

serve: ## 本地预览（热重载）
	mkdocs serve --open

build: ## 构建静态站点
	mkdocs build --strict

clean: ## 清理构建产物
	rm -rf site/

lint: ## 检查内容健康度
	python3 scripts/lint_content.py --docs-dir docs/

new-post: ## 创建新博客文章 (usage: make new-post TITLE="文章标题")
	@if [ -z "$(TITLE)" ]; then echo "Usage: make new-post TITLE=\"文章标题\""; exit 1; fi
	@DATE=$$(date +%Y-%m-%d); \
	SLUG=$$(echo "$(TITLE)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-'); \
	FILE="docs/blog/posts/$${DATE}-$${SLUG}.md"; \
	echo "---" > $$FILE; \
	echo "date: $${DATE}" >> $$FILE; \
	echo "authors:" >> $$FILE; \
	echo "  - gy-hou" >> $$FILE; \
	echo "categories:" >> $$FILE; \
	echo "  - 待分类" >> $$FILE; \
	echo "tags:" >> $$FILE; \
	echo "  - 待填写" >> $$FILE; \
	echo "---" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "# $(TITLE)" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "<!-- more -->" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "正文内容..." >> $$FILE; \
	echo "Created: $$FILE"

deploy: ## 手动部署（通常用 CI 自动部署）
	mkdocs gh-deploy --force

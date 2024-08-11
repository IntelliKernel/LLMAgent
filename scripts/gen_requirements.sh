# 创建临时目录
temp_dir=$(mktemp -d)

# 复制所有 Git 跟踪的 Python 文件到临时目录
git ls-files | grep '\.py$' | xargs -I {} cp --parents {} "$temp_dir"

# 在临时目录上运行 pipreqs
pipreqs "$temp_dir" --force

# 将生成的 requirements.txt 文件移动到项目根目录
mv "$temp_dir/requirements.txt" .

# 删除临时目录
rm -rf "$temp_dir"
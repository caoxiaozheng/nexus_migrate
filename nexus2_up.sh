#!/bin/bash

# 设置Nexus仓库信息和maven配置中的settings.xml文件相对应
nexus_repo_url=""
nexus_username=""
nexus_password=""
repositoryId=""

# 指定POM文件所在的目录
pom_directory="/data/maven2_snapshots/"
# 指定成功和失败日志文件路径
success_log_file="upload_success.log"
failure_log_file="upload_failure.log"

# 创建空的成功和失败日志文件
> $success_log_file
> $failure_log_file

# Maven上传函数
function upload_to_nexus() {
  local file=$1
  local group_id=$2
  local artifact_id=$3
  local version=$4
  local packaging=$5

  mvn deploy:deploy-file \
    -Durl=$nexus_repo_url \
    -Dfile=$file \
    -DgroupId=$group_id \
    -DartifactId=$artifact_id \
    -Dversion=$version \
    -Dpackaging=$packaging \
    -DgeneratePom=false \
    -DrepositoryId=$repositoryId

  # 检查Maven命令执行结果
  if [ $? -eq 0 ]; then
    # 记录上传成功的信息到成功日志文件
    echo "Upload succeeded for $file" >> $success_log_file
  else
    # 记录上传不成功的信息到失败日志文件
    echo "Upload failed for $file" >> $failure_log_file
  fi
}

# 遍历所有POM文件
for pom_file in $pom_directory/*.pom; do
  # 提取groupId和artifactId信息
  group_id=$(xmlstarlet sel -N x=http://maven.apache.org/POM/4.0.0 -t -v "/x:project/x:groupId" $pom_file)
  artifact_id=$(xmlstarlet sel -N x=http://maven.apache.org/POM/4.0.0 -t -v "/x:project/x:artifactId" $pom_file)
  version=$(xmlstarlet sel -N x=http://maven.apache.org/POM/4.0.0 -t -v "/x:project/x:version" $pom_file)


  if [ -z "$version" ]; then
    # 从JAR文件名称中提取版本号
    version_from_pom=$(echo $pom_directory/$pom_file | sed -n 's/.*-\([0-9]\+\.[0-9]\+\.[0-9]\+\)\.pom/\1/p')
    version=$version_from_pom
  fi

  # 获取对应的JAR文件名
  jar_file="${artifact_id}-${version}.jar"
  echo $group_id $artifact_id $version  $jar_file >> maven_qx.log

  # 检查JAR文件是否存在
  if [ -e "$jar_file" ]; then
    # 上传JAR文件
    upload_to_nexus $pom_directory/$jar_file  $group_id $artifact_id $version "jar"
  fi

  # 上传POM文件
  upload_to_nexus $pom_file  $group_id $artifact_id $version "pom"

  echo "Finished processing $pom_file"
done

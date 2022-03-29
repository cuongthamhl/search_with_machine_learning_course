mkdir -p /workspace/kaggle
touch /workspace/kaggle/kaggle.json
chmod 600 /workspace/kaggle/kaggle.json
cd docker
docker-compose pull
echo "pyenv activate search_with_ml_week2" >> ~/.bashrc

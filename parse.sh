cd parsers
while [[ true ]]
do
D:/Anaconda/envs/PyCharnEnv/python.exe parse_rbk.py
D:/Anaconda/envs/PyCharnEnv/python.exe parse_buhgalter.py
D:/Anaconda/envs/PyCharnEnv/python.exe parse_forbes.py
D:/Anaconda/envs/PyCharnEnv/python.exe merge_data.py
D:/Anaconda/envs/PyCharnEnv/python.exe predict_categories.py
echo "Data merged! Nap time"
sleep 18000
done
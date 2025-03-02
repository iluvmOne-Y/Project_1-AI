if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install python3 -y
    sudo apt install python3-pip -y
    sudo apt install python3-pygame -y
    sudo apt install python3-psutil -y
    sudo apt install python3-pandas -y
    sudo apt install python3-reportlab -y
    sudo apt install python3-matplotlib -y

elif [[ "$OSTYPE" == "win32"* ]] || [[ "$OSTYPE" == "cygwin"* ]] || [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo $OSTYPE
    pip install pygame
    pip install psutil
    pip install pandas
    pip install reportlab
    pip install matplotlib

fi
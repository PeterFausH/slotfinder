echo .
curl -i -XPOST http://192.168.200.223:8086/write?db=home --data-binary "sensor,ort=$1 state=$2"
echo .

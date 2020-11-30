for month in 08 09 10 11; do
  total_time=`cat test.csv | grep "2020-${month}" | cut -d',' -f 5 | awk '{s+=$1} END {print s}'`
  slots=`cat test.csv | grep "2020-$"`
  echo "Month ${month}, time ${total_time}"
done

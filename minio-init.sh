until (/usr/bin/mc config host add myminio http://minio:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY")
do
  echo "MinIO connection waiting..."
  sleep 1
done

/usr/bin/mc mb "myminio/$MINIO_BUCKET_NAME" || true
/usr/bin/mc anonymous set download "myminio/$MINIO_BUCKET_NAME"
/usr/bin/mc anonymous set public "myminio/$MINIO_BUCKET_NAME"
echo "Bucket $MINIO_BUCKET_NAME is now public!"
git add .
git commit -m "Shuai Commit"
git push -u origin main
kubectl delete -f k8s/service_test/unit/test_identity.yaml
sleep 3
kubectl apply -f k8s/service_test/unit/test_identity.yaml
sleep 2
kubectl logs identity-test -f

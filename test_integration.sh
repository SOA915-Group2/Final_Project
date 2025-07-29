git add .
git commit -m "Shuai Commit"
git push -u origin main
kubectl delete -f k8s/service_test/integration/test_integration.yaml
sleep 3
kubectl apply -f k8s/service_test/integration/test_integration.yaml
sleep 2
kubectl logs integration-test -f

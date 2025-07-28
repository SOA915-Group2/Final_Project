git add .
git commit -m "Shuai Commit"
git push -u origin main
kubectl delete -f k8s/deployments/test-runner.yaml
sleep 3
kubectl apply -f k8s/deployments/test-runner.yaml
sleep 2
kubectl logs identity-test -f

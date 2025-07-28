git add .
git commit -m "Shuai Commit"
git push -u origin main
kubectl delete -f k8s/deployments/test-runner.yaml
kubectl apply -f k8s/deployments/test-runner.yaml
kubectl logs identity-test -f

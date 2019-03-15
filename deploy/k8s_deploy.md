## K8S DEPLOYMENT

### __pull source code__

```
git clone ssh://git@gitlab.cloud.enndata.cn:10885/xujieasd/impala_rest.git
```

### __build docker image__

```
docker build -t xujieasd/impala_rest:0.2
```

### __create deployment and service__

__(1) simple deployment__ 

- You can find example deployment file __[HERE](./yaml/impala-rest-dep-simple.yaml)__
- Note:  

You need to fill in args for `type` (common/adjust) and `admin` (admin code)  
like:
```yaml
args:
  - "--type adjust"
  - "--admin admin"

```

- Expose deployment after pod created:

```
kubectl create -f impala-rest-dep-simple.yaml
kubectl expose deployment/impala-rest --type=NodePort
kubectl get svc -o wide
NAME           CLUSTER-IP       EXTERNAL-IP                         PORT(S)          AGE       SELECTOR

impala-rest    10.99.69.43      <nodes>                             5000:30047/TCP   5h        run=impala-rest
kubernetes     10.96.0.1        <none>                              443/TCP          42d       <none>
```

__(2) deploy with comfigMap__

- Write configMap file

you can find example configMap file __[HERE](./yaml/impala-rest-configm.yaml)__  

```
kubectl create -f impala-rest-configm.yaml
```

- Create deployment and expose service

you can find example deployment file __[HERE](./yaml/impala-rest-dep-configMap.yaml)__

```
kubectl create -f impala-rest-dep-comfigMap.yaml
kubectl expose deployment/impala-rest --type=NodePort
```

__(3) deploy with cephfs__

- first you must have ceph on your cluster
- create secret, pv and pvc, __[OFFICIAL REFERENCE](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)__
- create deployment and expose service __[REFERENCE](./yaml/impala-rest-dep-cephfs.yaml)__


### __call restful api__

e.g:

```
curl -i -X GET http://10.19.138.90:30047/sql_list
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 94
Server: Werkzeug/0.14.1 Python/2.7.6
Date: Fri, 10 Aug 2018 08:49:20 GMT

["sql_join1", "sql_join2", "sql_select2", "sql_select3", "sql_select1", "sql_describe_table"]
```




---
title: kubectl
date: 2018-10-31T12:00:00-04:00
tags:
  - tech
---

The `kubectl` command combined with `jq` is the Swiss Army Chainsaw of
kubernetes management. Some of my more useful `kubectl` commands:

```bash
  watch 'kubectl get pods | column'

  # Delete all failed pods.
  kubectl get pods --field-selector=status.phase=Failed -o json | jq -r '.items[] .metadata.name'  | xargs kubectl delete pod

  # All images running that have the word 'dirty' in their name.
  kubectl get pods -o json | jq -r '..|.containerStatuses?|select(.!=null)|.[].image' | sort | uniq | grep dirty
```

<a href="https://brid.gy/publish/twitter"></a>

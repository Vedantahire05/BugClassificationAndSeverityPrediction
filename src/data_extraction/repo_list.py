# BASE (ML + Infra + Frontend)
REPOSITORIES_BASE = [
    "kubernetes/kubernetes",
    "tensorflow/tensorflow",
    "pytorch/pytorch",
    "docker/docker",
    "numpy/numpy",
    "pandas-dev/pandas",
    "scikit-learn/scikit-learn",
    "nodejs/node",
    "vercel/next.js",
]

# UI / RENDER (PR enabled)
REPOSITORIES_UI = [
    "microsoft/vscode",
    "electron/electron",
    "facebook/react",
    "mozilla/gecko-dev",
]

# SECURITY
REPOSITORIES_SECURITY = [
    "openssl/openssl",
    "cilium/cilium",
    "OWASP/juice-shop",
    "metasploit/metasploit-framework",
    "zaproxy/zaproxy",
]

# COMPILER / CRASH
REPOSITORIES_CRASH = [
    "rust-lang/rust",
    "llvm/llvm-project",
    "python/cpython",
    "flutter/flutter",
]

# PERFORMANCE (PR enabled)
REPOSITORIES_PERFORMANCE = [
    "chromium/chromium",
    "google/benchmark",
    "google/tcmalloc",
]

# STORAGE / DB (NEW)
REPOSITORIES_STORAGE = [
    "etcd-io/etcd",
    "redis/redis",
    "cockroachdb/cockroach",
    "tikv/tikv",
    "influxdata/influxdb",
]

# NETWORK / DISTRIBUTED SYSTEMS (NEW)
REPOSITORIES_NETWORK = [
    "envoyproxy/envoy",
    "grpc/grpc",
    "apache/kafka",
    "apache/cassandra",
    "hashicorp/consul",
]

# MIXED (Infra + Tracing + Orchestration)
REPOSITORIES_MIXED = [
    "prometheus/prometheus",
    "kubernetes/minikube",
    "containerd/containerd",
    "istio/istio",
    "jaegertracing/jaeger",
]

# ORDER (start from Domain D)
REPOSITORIES_ORDERED = (
    REPOSITORIES_STORAGE +
    REPOSITORIES_NETWORK +
    REPOSITORIES_MIXED 
)

# PR TARGET DOMAINS
PR_REPOS = REPOSITORIES_UI + REPOSITORIES_PERFORMANCE

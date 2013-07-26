upstream app {
    # For a TCP configuration:
    server <%=app%> fail_timeout=0;
}

server {
    listen 80 default;
    client_max_body_size 4G;
    server_name _;

    keepalive_timeout 5;

    # Enable gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_buffers 16 8k;
    gzip_disable "MSIE [1-6].(?!.*SV1)";
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    <%- if auth -%>
    # password-protect site
    auth_basic "Restricted";
    auth_basic_user_file htpasswd-<%= name %>;
    <%- end -%>

    location /static {
        alias /srv/www/app/app/static;

        expires max;
        add_header Pragma cache;
        add_header cache-control public;
    }

    location /repository {
        internal;
        alias /srv/www/app/app/data/repository;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        proxy_pass   http://app;
    }
}

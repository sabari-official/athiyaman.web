# Athiyaman Platform - Deployment Implementation Document
## Phase 1 – Digital India Production Deployment & DevOps Runbooks

---

## 1. Linux Setup

*   **Operating System:** Enforces Ubuntu 22.04 LTS or CentOS 8 distributions, locked to $64\text{-bit}$ architectures.
*   **System Update & Essential Packages:** Apply security updates and install essential packages:
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y curl git ufw fail2ban htop python3-pip python3-venv certbot
    ```
*   **Process Limit Optimizations:** Edit `/etc/security/limits.conf` to increase maximum open file descriptors:
    ```ini
    * soft nofile 65535
    * hard nofile 65535
    ```

---

## 2. DirectAdmin Setup

*   **Virtual Host Allocations:** Assign dedicated directories under the user accounts folder to separate static asset files from API routes:
    *   *Frontend static directory:* `/home/athiyaman/domains/athiyaman.in/public_html`
    *   *Backend repository path:* `/home/athiyaman/app/backend`
*   **Process Managers Configurations:** Standardize DirectAdmin cron schedules to execute server cleanups and rotate logs during off-peak hours ($3\text{:00 AM}$).

---

## 3. Domain & Subdomain Setup

*   **DNS Mapping Rules:** Map subdomains to production host IPs using DirectAdmin DNS managers:
    *   `athiyaman.in` $\rightarrow$ A record pointing to static edge CDN servers (Vercel).
    *   `api.athiyaman.in` $\rightarrow$ A record pointing to the application server IP.
    *   `staging.athiyaman.in` $\rightarrow$ A record pointing to the staging server IP.
*   **TTL Configuration Strategy:** Configure TTL thresholds (default $300\text{ seconds}$) to support quick DNS changes during maintenance events.

---

## 4. SSL Setup

*   **Let's Encrypt certificates:** Enable automated Let's Encrypt certificates via DirectAdmin to enforce secure HTTPS traffic:
    ```bash
    # Generate and test certbot certificate generation
    sudo certbot certonly --standalone -d api.athiyaman.in -d staging.athiyaman.in
    ```
*   **Automatic Certificate Renewal:** Certbot handles certificate renewals automatically:
    ```bash
    # Verify renewal script crons
    sudo certbot renew --dry-run
    ```

---

## 5. PostgreSQL Setup

*   **PostgreSQL Installation:** Install and configure PostgreSQL v15+ on standard database servers:
    ```bash
    sudo apt install -y postgresql-15 postgresql-contrib-15
    ```
*   **Role Provisioning:** Create a dedicated, unprivileged database owner user account (`athiyaman_db_user`), avoiding standard administrative accounts:
    ```sql
    CREATE USER athiyaman_db_user WITH PASSWORD 'SecureDatabasePassword123!';
    CREATE DATABASE athiyaman_digital_india OWNER athiyaman_db_user;
    ```
*   **PgBouncer Pool Configurations:** Configure PgBouncer pool settings in `/etc/pgbouncer/pgbouncer.ini` under port $6432$ to manage database connection pools:
    ```ini
    [databases]
    athiyaman_digital_india = host=127.0.0.1 port=5432 dbname=athiyaman_digital_india
    
    [pgbouncer]
    listen_port = 6432
    listen_addr = 127.0.0.1
    auth_type = md5
    auth_file = /etc/pgbouncer/userlist.txt
    pool_mode = transaction
    max_client_conn = 1000
    default_pool_size = 50
    ```

---

## 6. Backend Deployment

*   **Repository Cloning:** Clone the production repository in the backend app directory:
    ```bash
    git clone https://github.com/athiyaman/backend.git /var/www/athiyaman/backend
    cd /var/www/athiyaman/backend
    ```
*   **Virtual Environment Setup:** Create and activate a Python virtual environment to manage backend dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
*   **Alembic Database Migrations:** Run Alembic migration scripts to upgrade production database schemas sequentially:
    ```bash
    alembic upgrade head
    ```
*   **Systemd Application Controller Setup:** Deploy the FastAPI backend under Gunicorn/Uvicorn, managing process lifecycles via Systemd:
    ```bash
    sudo nano /etc/systemd/system/athiyaman.service
    ```
    ```ini
    [Unit]
    Description=Athiyaman FastAPI Application Server
    After=network.target
    
    [Service]
    User=athiyaman_user
    WorkingDirectory=/var/www/athiyaman/backend
    ExecStart=/var/www/athiyaman/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=multi-user.target
    ```
    ```bash
    sudo systemctl enable athiyaman
    sudo systemctl start athiyaman
    ```

---

## 7. Frontend Deployment

*   **React Asset Compilation:** Compile frontend assets into highly optimized, minified bundles, stripping debugging console logs:
    ```bash
    npm install
    npm run build
    ```
*   **Asset Delivery Setup:** Copy compiled assets to the public web server directory:
    ```bash
    cp -r dist/* /var/www/athiyaman/frontend/
    ```

---

## 8. Environment Variables Configuration

Backend configurations are loaded from secure `.env` files using Pydantic Settings, keeping credentials out of repositories:

```ini
DATABASE_URL=postgresql+psycopg2://db_user:secure_pwd@127.0.0.1:6432/athiyaman_digital_india
JWT_SECRET=super_secret_cryptographic_key_32_bytes_min
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
STORAGE_TYPE=LOCAL
STORAGE_PATH=/var/www/athiyaman/uploads
GOOGLE_MAPS_KEY=gmaps_api_credential_key
```

---

## 9. Nginx Configuration

NGINX handles static files, manages SSL configurations, and proxies API requests to the application server:

```nginx
server {
    listen 80;
    server_name api.athiyaman.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.athiyaman.in;

    ssl_certificate /etc/letsencrypt/live/api.athiyaman.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.athiyaman.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self';" always;

    # Static Assets Caching
    location /static/ {
        alias /var/www/athiyaman/backend/static/;
        expires 1y;
        add_header Cache-Control "public, no-transform";
    }

    # API Proxy Routing
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 10. Monitoring Setup

*   **Prometheus & Grafana:** Install Prometheus and Grafana on standard metrics servers, configuring Grafana to display server diagnostics:
    *   Tracks CPU usage, memory utilization, and active database connection pool stats.
*   **Sentry Crash Integrations:** Configure Sentry SDK key variables inside `.env` configurations to route application exceptions to developers.

---

## 11. Backup Setup

*   **Daily Full Backups Cron:** Run automated pg_dump scripts daily during off-peak hours ($2\text{:00 AM}$):
    ```bash
    sudo nano /etc/cron.daily/athiyaman_db_backup
    ```
    ```bash
    #!/bin/bash
    BACKUP_DIR="/var/www/athiyaman/backups"
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    pg_dump -U athiyaman_db_user -h 127.0.0.1 -p 6432 athiyaman_digital_india | gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz
    
    # Prune backups older than 30 days
    find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +30 -delete
    ```
    ```bash
    chmod +x /etc/cron.daily/athiyaman_db_backup
    ```

---

## 12. Queue Worker Setup

Heavy background tasks use Celery workers managed via Redis queues:

*   **Celery Background Service Setup:** Configure Systemd process controllers to manage background workers:
    ```bash
    sudo nano /etc/systemd/system/athiyaman-worker.service
    ```
    ```ini
    [Unit]
    Description=Celery Worker for Athiyaman Queue
    After=network.target redis.service
    
    [Service]
    User=athiyaman_user
    WorkingDirectory=/var/www/athiyaman/backend
    ExecStart=/var/www/athiyaman/backend/venv/bin/celery -A app.jobs.tasks worker --loglevel=info
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```
    ```bash
    sudo systemctl enable athiyaman-worker
    sudo systemctl start athiyaman-worker
    ```

---

## 13. Security Hardening

*   **UFW Firewall Rules:** Enable UFW firewalls, keeping active database ports inaccessible from external networks:
    ```bash
    sudo ufw allow 22/tcp  # SSH port
    sudo ufw allow 80/tcp  # HTTP port
    sudo ufw allow 443/tcp # HTTPS port
    sudo ufw default deny incoming
    sudo ufw enable
    ```
*   **Fail2Ban Configuration:** Configure Fail2Ban to block brute-force attempts targeting port 22.
*   **SSH Security Hardening:** Disable root user logins and configure SSH key-based access controls.

---

## 14. Production Validation

*   **Health Checks Validation:** API endpoint `/api/v1/health` checks database connectivity and backend service status.
*   **Visual Layouts Audits:** Check that unprivileged users receive `403 Forbidden` errors when accessing `/api/v1/admin/*` endpoints.

---

## 15. Rollback Procedures

If a production update fails, the DevOps team rolls back the application code and database schema to the latest stable release:

```bash
# 1. Stop active Systemd services
sudo systemctl stop athiyaman
sudo systemctl stop athiyaman-worker

# 2. Revert application code to the latest stable release
cd /var/www/athiyaman/backend
git reset --hard HEAD~1

# 3. Revert database schema modifications
source venv/bin/activate
alembic downgrade HEAD~1

# 4. Restart application services
sudo systemctl start athiyaman
sudo systemctl start athiyaman-worker
```

---

## 16. Disaster Recovery Procedures

*   **Database Recovery Restores:** Restore database states using daily full backups and hourly WAL logs:
    ```bash
    # 1. Stop database service
    sudo systemctl stop postgresql
    
    # 2. Extract database backups
    gunzip -c /var/www/athiyaman/backups/db_backup_target_date.sql.gz > /tmp/db_restore.sql
    
    # 3. Restore data structures
    psql -U athiyaman_db_user -h 127.0.0.1 -p 6432 -d athiyaman_digital_india -f /tmp/db_restore.sql
    
    # 4. Restart services
    sudo systemctl start postgresql
    ```
*   **Relational Integrity checks:** Run validation scripts to check keys and relational constraints after a restore.

---

## 17. Go-Live Checklist

Before launching Phase 1, ensure all items on this go-live checklist are completed:

- [ ] **Infrastructure Vetting:** Confirm all port blocks are configured and NGINX redirects HTTP traffic successfully.
- [ ] **SSL Configuration:** Verify SSL certificates are active, enforcing secure HTTPS traffic.
- [ ] **Database Connection:** Confirm database instances run locally and PgBouncer connection pool managers are active.
- [ ] **Secrets Security:** Verify environmental secrets are loaded securely from external environments.
- [ ] **Audit Logging:** Verify trigger functions block UPDATE and DELETE queries on audit logs.
- [ ] **Daily Backups:** Confirm automated pg_dump scripts run daily and WAL logs are active.
- [ ] **Monitoring Setup:** Confirm Grafana dashboard displays server diagnostics and Sentry integrations are active.
- [ ] **Rollback Validation:** Verify database rollbacks and application container rollback scripts run successfully.

---

## 18. Conclusion

This Deployment Implementation Document (`15_DEPLOYMENT_IMPLEMENTATION.md`) establishes the absolute infrastructure setups, NGINX proxy configs, Let's Encrypt SSL certificates, Celery workers, cron backups, rollback procedures, and go-live checklists for the Athiyaman Platform – Digital India Phase 1. By detailing server configurations and providing complete SQL and shell scripts, it serves as a complete technical guide for DevOps and system engineers, ensuring a secure, reliable, and scalable production deployment.

FROM public.ecr.aws/glue/aws-glue-libs:5

# Switch to root user to install packages
USER root

# Install Jupyter Lab and other useful packages using the system's Python
RUN /usr/bin/python3.11 -m pip install --no-cache-dir \
    jupyterlab \
    notebook \
    ipykernel \
    matplotlib \
    seaborn \
    pandas \
    plotly

# Create a jupyter config directory for hadoop user
RUN mkdir -p /home/hadoop/.jupyter && \
    chown -R hadoop:hadoop /home/hadoop/.jupyter

# Create a simple script to start jupyter
RUN echo '#!/bin/bash' > /usr/local/bin/start-jupyter && \
    echo 'cd /home/hadoop/workspace' >> /usr/local/bin/start-jupyter && \
    echo '/usr/bin/python3.11 -m jupyterlab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --IdentityProvider.token="" --ServerApp.password="" --ServerApp.allow_origin="*"' >> /usr/local/bin/start-jupyter && \
    chmod +x /usr/local/bin/start-jupyter

# Expose port 8888 for Jupyter Lab
EXPOSE 8888

# Switch back to hadoop user
USER hadoop

# Set working directory
WORKDIR /home/hadoop/workspace

# Default command
CMD ["/usr/local/bin/start-jupyter"]

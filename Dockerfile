FROM ubuntu:22.04

ENV RUNNING_IN_DOCKER true

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install gnupg wget curl git -y 

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs

# Install Google Chrome
RUN  wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends

# Install Oh My Zsh
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.0/zsh-in-docker.sh)" -- \
  -t https://github.com/denysdovhan/spaceship-prompt \
  -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
  -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
  -p git \
  -p ssh-agent \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions

RUN apt-get --fix-broken install -y \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY ./install_packages.sh ./

RUN chmod +x ./install_packages.sh

SHELL ["/bin/zsh", "-c"]

CMD ["/bin/zsh"]

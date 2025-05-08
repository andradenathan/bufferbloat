## Bufferbloat

O **bufferbloat** é um fenômeno em redes de computadores no qual *buffers* excessivamente grandes em roteadores e switches causam alta latência e degradação geral do desempenho de rede.

---

### 📋 Sumário

1. [Objetivo](#objetivo)
2. [Descrição do Projeto](#descri%C3%A7%C3%A3o-do-projeto)

   * [Parte 1: Preparação do Ambiente](#parte-1-prepara%C3%A7%C3%A3o-do-ambiente)
   * [Parte 2: Experimento com TCP Reno](#parte-2-experimento-com-tcp-reno)
   * [Parte 3: Experimento com TCP BBR](#parte-3-experimento-com-tcp-bbr)
   * [Parte 4: Experimento com QUIC](#parte-4-experimento-com-quic)
3. [Mini-Projeto de Análise Experimental](#mini-projeto-de-an%C3%A1lise-experimental)
4. [Referências](#refer%C3%AAncias)

---

## Objetivo

Estudar e comparar o impacto do bufferbloat em diferentes protocolos de transporte (TCP Reno, TCP BBR e QUIC) utilizando o Mininet como ambiente de emulação de rede.

---

## Descrição do Projeto

### Parte 1: Preparação do Ambiente

1. Provisionar uma máquina virtual com Mininet (via Vagrant).
2. Clonar o repositório inicial para o experimento.

### Parte 2: Experimento com TCP Reno

* Configurar uma topologia Mininet com link de uplink de baixa largura de banda.
* Implementar conexões usando **TCP Reno**.
* Preencher os trechos marcados como `TODO` no código-base.
* Executar o script de medição e coletar métricas de latência e throughput.
* Responder às questões propostas com base nos resultados obtidos.

### Parte 3: Experimento com TCP BBR

* Repetir a mesma topologia da Parte 2.
* Trocar o congestion control para **TCP BBR**.
* Gerar e comparar os resultados de latência e throughput em relação ao TCP Reno.

### Parte 4: Experimento com QUIC

* Implementar o mesmo cenário usando o protocolo **QUIC** (via biblioteca *aioquic*).
* Coletar métricas de desempenho.
* Comparar com os resultados de TCP Reno e TCP BBR.

---

## Mini-Projeto de Análise Experimental

* Criar scripts para automatizar a coleta de dados para os três protocolos.
* Gerar gráficos comparativos de latência, jitter e throughput.
* Elaborar relatório apontando vantagens e desvantagens de cada protocolo sob condições de bufferbloat.

---

## Referências

* [mininet-vagrant](https://github.com/skywardpixel/mininet-vagrant)
* [aioquic (QUIC implementation)](https://github.com/aiortc/aioquic)



## Autores

<a href="https://github.com/andradenathan">
    <img src="https://avatars.githubusercontent.com/u/42661561?v=4" width="150px"/>
</a>
<a href="https://github.com/0nerb">
    <img src="https://avatars.githubusercontent.com/u/126625129?v=4" width="150px" />
</a>
<a href="https://github.com/MMuhen">
    <img src="https://avatars.githubusercontent.com/u/139181000?v=4" width="150px" />
</a>


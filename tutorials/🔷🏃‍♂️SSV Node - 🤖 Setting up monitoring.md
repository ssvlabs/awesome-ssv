# 🔷🏃‍♂️SSV Node - 🤖 Setting up monitoring

[![🔷🏃‍♂️SSV Node - 🤖 Setting up monitoring](http://img.youtube.com/vi/4KLgI42zidg/0.jpg)](https://www.youtube.com/watch?v=4KLgI42zidg "🔷🏃‍♂️SSV Node - 🤖 Setting up monitoring")

**DISCLAIMER**
The content provided is for informational purposes only and should not be considered as professional advice. The information presented may not be complete, accurate or up-to-date. The reader or viewer is solely responsible for any actions taken based on the information provided. The author and publisher shall not be held liable for any losses, damages or injuries arising from the use of the information provided. It is recommended to seek professional advice for specific situations.

## Credits 

Great thanks goes to [@Taiga](https://twitter.com/zkTaiga) for making all the necessary changes to the original `eth-docker` stack to make the monitoring work! 
and 
[@Yorick](https://twitter.com/cryptomanuf) who has helped me with setting up nodes, `eht-docker` and staking stuff in general! 

### What will you do
The video is walking through setting up **monitoring**(SSV+EL+CL) using eth-docker prometheus and grafana.  
For more info follow the [official documentation](https://docs.ssv.network/run-a-node/operator-node/installation).

## Steps

Follow along with the video. 

	1. add new job to `/eth-docker/prometheus/custom-prom.yml` 
 		Name it the same as the ssv container
	2. import dasboard to grafana 
	3. edit dashboard 
		- datasource may be wrong, if so:
		find correct data source `"uid":"DSFIJO.."`
		edit dasboard
			JSON Model
				replace all datasources with correct ones 
			Variables 
				add your instance here
				you should see it in "Preview of values" field 
				
### Useful code 



```bash
 ssh user@82.999.000.000 -L 3000:127.0.0.1:3000 #expose_graphana_port_locally
```


```yml
  - job_name: ssv_nodes
    metrics_path: /metrics
    static_configs:
      - targets:
        - lido-ssv-node:15000

  - job_name: ssv_nodes_health
    metrics_path: /health
    static_configs:
      - targets:
        - lido-ssv-node:15000

```

Regex:
```
/([a-z0-9-]+):/

```


## Other video tutorials

[See other tutorials](https://www.youtube.com/channel/UCD7q4qIhrhFjEhSxGdLR-CQ)

## Reach out 

[SSV discord](https://discord.gg/invite/ssvnetworkofficial)
 - `# operators-general` channel 

## Other tutorials 

[markoInEther youtube channel](https://www.youtube.com/channel/UCD7q4qIhrhFjEhSxGdLR-CQ)




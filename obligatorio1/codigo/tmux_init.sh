SESSION="redes_2025"

sudo tmux new-session -d -s $SESSION -n A "~/redes2025_ob1/config.sh; bash"

sudo sleep 5

sudo tmux new-window -t $SESSION:1 -n B "~/redes2025_ob1/run_mininet.sh; bash"

sudo sleep 5

sudo tmux new-window -t $SESSION:2 -n C "~/redes2025_ob1/run_pox.sh; bash"

sudo sleep 5

sudo tmux new-window -t $SESSION:3 -n vhost1 "~/redes2025_ob1/run_sr.sh 127.0.0.1 vhost1; bash"
sudo tmux new-window -t $SESSION:4 -n vhost2 "~/redes2025_ob1/run_sr.sh 127.0.0.1 vhost2; bash"
sudo tmux new-window -t $SESSION:5 -n vhost3 "~/redes2025_ob1/run_sr.sh 127.0.0.1 vhost3; bash"
sudo tmux new-window -t $SESSION:6 -n vhost4 "~/redes2025_ob1/run_sr.sh 127.0.0.1 vhost4; bash"
sudo tmux new-window -t $SESSION:7 -n vhost5 "~/redes2025_ob1/run_sr.sh 127.0.0.1 vhost5; bash"

sudo tmux attach -t $SESSION

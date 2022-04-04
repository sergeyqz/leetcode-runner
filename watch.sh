#/usr/bin/env sh
inotifywait -m $1 --include '^.*\.(py|testcases)$' -e close_write |
    while read dir action file
    do
        file=${file%%.*}
        echo Run $file
	systemd-run --user -G --pty --quiet --same-dir time -f '%U %S %E %M' $(which timeout) 5s $(which python) runner.py $dir $file
        case $? in
            0)
                echo OK
                ;;
            1)
                echo WA
                ;;
            2)
                echo SyntaxError
                ;;
            3)
                echo Error
                ;;
            124)
                echo TLE $file
                ;;
        esac
    done

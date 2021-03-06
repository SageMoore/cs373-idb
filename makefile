FILES :=                              \
    model.html                      \
    models.py                        \
    apiary.apib                      \
    IDB1.log                       \
    crimecast.py                        \
    tests.py                          \
    UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  model.html
	rm -f  IDB1.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: crimecast_test.tmp

model.html: models.py
	pydoc -w models

IDB3.log:
	git log > IDB3.log

crimecast-test.tmp: tests.py
	coverage3 run    --branch tests.py >  crimecast-test.tmp 2>&1
	coverage3 report -m --include="./*"                     >> crimecast-test.tmp
	cat crimecast-test.tmp
	rm crimecast-test.tmp

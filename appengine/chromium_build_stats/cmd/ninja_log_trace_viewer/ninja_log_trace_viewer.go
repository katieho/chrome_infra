// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// ninja_log_trace_viewer converts .ninja_log into trace-viewer formats.
//
// usage:
//  $ ../../goenv.sh goapp run ninja_log_trace_viewer.go --filename out/Release/.ninja_log
//
//  $ ../../goenv.sh goapp run ninja_log_trace_viewer.go \
//    --filename out/Release/.ninja_log --port 1234
//
package main

import (
	"bufio"
	"compress/gzip"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"time"

	"ninjalog"
	"ninjalog/traceviewer"
)

var (
	filename             = flag.String("filename", ".ninja_log", "filename of .ninja_log")
	traceJSON            = flag.String("trace_json", "trace.json", "output filename as trace.json")
	traceViewerTmplFname = flag.String("trace_viewer_tmpl", "../../default/tmpl/trace-viewer.html", "path of trace-viewer.html template generated by gen-trace-viewer.sh")
	port                 = flag.Int("port", 0, "port number to listen http")
	browser              = flag.String("browser", "x-www-browser", "browser to launch")
)

func reader(fname string, rd io.Reader) (io.Reader, error) {
	if filepath.Ext(fname) != ".gz" {
		return bufio.NewReaderSize(rd, 512*1024), nil
	}
	return gzip.NewReader(bufio.NewReaderSize(rd, 512*1024))
}

func convert(fname string) ([]ninjalog.Trace, error) {
	f, err := os.Open(fname)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	rd, err := reader(fname, f)
	if err != nil {
		return nil, err
	}

	njl, err := ninjalog.Parse(fname, rd)
	if err != nil {
		return nil, err
	}
	steps := ninjalog.Dedup(njl.Steps)
	flow := ninjalog.Flow(steps)
	return ninjalog.ToTraces(flow, 1), nil
}

func output(fname string, traces []ninjalog.Trace) (err error) {
	f, err := os.Create(fname)
	if err != nil {
		return err
	}
	defer func() {
		cerr := f.Close()
		if err == nil {
			err = cerr
		}
	}()
	js, err := json.Marshal(traces)
	if err != nil {
		return err
	}
	_, err = f.Write(js)
	return err
}

func traceHTML(fname string, traces []ninjalog.Trace) (func(http.ResponseWriter, *http.Request), error) {
	t, err := traceviewer.Parse(*traceViewerTmplFname)
	if err != nil {
		return nil, err
	}
	b, err := t.HTML(fname, traces)
	if err != nil {
		return nil, err
	}
	return func(w http.ResponseWriter, req *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.WriteHeader(http.StatusOK)
		_, err = w.Write(b)
		if err != nil {
			log.Panic(err)
		}
	}, nil
}

func main() {
	flag.Parse()

	traces, err := convert(*filename)
	if err != nil {
		log.Fatal(err)
	}
	if *traceJSON != "" {
		err = output(*traceJSON, traces)
		if err != nil {
			log.Fatal(err)
		}
	}
	if *port == 0 {
		return
	}
	hf, err := traceHTML(*filename, traces)
	if err != nil {
		log.Fatal(err)
	}
	if *browser != "" {
		go func() {
			u := fmt.Sprintf("http://localhost:%d", *port)
			for {
				_, err := http.Get(u)
				if err == nil {
					break
				}
				fmt.Printf("waiting for %s", u)
				time.Sleep(1 * time.Second)
			}
			cmd := exec.Command(*browser, u)
			err := cmd.Run()
			if err != nil {
				log.Fatal(err)
			}
		}()
	}
	http.HandleFunc("/", hf)
	fmt.Printf("listening on :%d\n", *port)
	err = http.ListenAndServe(fmt.Sprintf(":%d", *port), nil)
	if err != nil {
		log.Fatal(err)
	}
}
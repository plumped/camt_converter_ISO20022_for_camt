For firefly-iii/data-importer (https://github.com/firefly-iii/data-importer) support a camt.zip to csv export is already in progress as quickwin workarround. It will be possible to load ziped camt packages from your bank directly into the converter for .csv output.

In a further step the direct connection to firefly-iii will be provided per interface or api

Docker install: Find image on https://hub.docker.com/r/plumpedboots/camt_converter

    docker pull plumpedboots/camt_converter:latest
    docker run -d -p 5000:5000 plumpedboots/camt_converter

or use the docker-compose file: https://github.com/plumped/camt_converter_ISO20022_for_camt/blob/master/docker-compose.yml

How to:
1. Visit your bank account.
2. Download as many CAMT reports as you like as a zip file
3. Upload zip-file to webapp using the "Browse..." button
4. CSV Files will be generated in background
5. Download your archive including all the csv files with the "Download archive" button.
6. Import it in firefly-iii/data-importer

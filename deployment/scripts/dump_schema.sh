#!/bin/bash

echo 'Dumping schema (without data) to mozio.sql'
pg_dump -s mozio > ../sql/mozio.sql

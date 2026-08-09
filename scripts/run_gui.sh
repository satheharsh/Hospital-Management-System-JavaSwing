#!/bin/bash
echo "Compiling and running Hospital Management System GUI..."
mvn clean compile exec:java -Dexec.mainClass="com.hospital.Main"

package com.hospital.util;

import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.nio.file.*;

public class IconConverter {
    public static void main(String[] args) {
        String resourcePath = "src/main/resources/images/";
        File resourceDir = new File(resourcePath);
        
        if (!resourceDir.exists()) {
            System.out.println("Creating resources directory...");
            resourceDir.mkdirs();
        }

        File[] svgFiles = resourceDir.listFiles((dir, name) -> name.toLowerCase().endsWith(".svg"));
        if (svgFiles != null && svgFiles.length > 0) {
            for (File svgFile : svgFiles) {
                try {
                    String pngFileName = svgFile.getName().replace(".svg", ".png");
                    convertSvgToPng(svgFile.getPath(), resourcePath + pngFileName);
                    System.out.println("Converted " + svgFile.getName() + " to PNG");
                } catch (Throwable e) {
                    System.err.println("Note: SVG conversion skipped for " + svgFile.getName() + " (" + e.getMessage() + ")");
                }
            }
        }
    }

    private static void convertSvgToPng(String svgPath, String pngPath) throws Exception {
        Class<?> pngTranscoderClass = Class.forName("org.apache.batik.transcoder.image.PNGTranscoder");
        Object transcoder = pngTranscoderClass.getDeclaredConstructor().newInstance();

        Class<?> transcoderInputClass = Class.forName("org.apache.batik.transcoder.TranscoderInput");
        Constructor<?> inputConst = transcoderInputClass.getConstructor(String.class);
        String svgURI = Paths.get(svgPath).toUri().toURL().toString();
        Object input = inputConst.newInstance(svgURI);

        Class<?> transcoderOutputClass = Class.forName("org.apache.batik.transcoder.TranscoderOutput");
        Constructor<?> outputConst = transcoderOutputClass.getConstructor(OutputStream.class);

        Method transcodeMethod = pngTranscoderClass.getMethod("transcode", transcoderInputClass, transcoderOutputClass);

        try (OutputStream outStream = new FileOutputStream(pngPath)) {
            Object output = outputConst.newInstance(outStream);
            transcodeMethod.invoke(transcoder, input, output);
        }
    }
}
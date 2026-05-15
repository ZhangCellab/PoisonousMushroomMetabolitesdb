package com.yy.mushroomtoxindb;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.yy.mushroomtoxindb.mapper")
public class MushroomToxinDbApplication {
    public static void main(String[] args) {
        SpringApplication.run(MushroomToxinDbApplication.class, args);
    }

}

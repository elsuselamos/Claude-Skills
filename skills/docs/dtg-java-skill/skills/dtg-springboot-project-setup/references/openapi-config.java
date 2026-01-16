// OpenAPI 配置
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("企业级微服务 API")
                        .version("2.7.0")
                        .description("Spring Boot 2.7 企业级微服务API文档")
                        .contact(new Contact()
                                .name("开发团队")
                                .email("dev@enterprise.com")))
                .components(new Components()
                        .addSecuritySchemes("bearerAuth",
                                new SecurityScheme()
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")))
                .addSecurityItem(new SecurityRequirement().addList("bearerAuth"));
    }
}

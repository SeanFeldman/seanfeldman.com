await Bootstrapper
    .Factory
    .CreateWeb(args)
    .AddSetting(
        Statiq.Markdown.MarkdownKeys.MarkdownExtensions,
        new List<string> 
        {
            "Bootstrap"
        })
    .RunAsync();
namespace project3_genetic_algorithms
{
    public struct PlayerConfiguration
    {
        public static int Periods { get; set; }
        public static double PlayerMaxHealth { get; set; }
        public static double PlayerStartingHealth { get; set; }
        public static double BaseHealthLoss { get; set; }
        public static double HealthLossPeriodModifier { get; set; }
        public static int MaxTotalWidth { get; set; }
        public static int MaxTotalHeight { get; set; }
        public static int MaxColumnsHarvested { get; set; }
        public static int StartingHarvestSize { get; set; }
        public static int StartingHarvestValue { get; set; }
        public static decimal HealthRegenerationConstant { get; set; }
        public static decimal RowGammaModifier { get; set; }
        public static decimal LifeEnjoymentConstant { get; set; }
        public static decimal LifeEnjoymentAlpha { get; set; }

        static PlayerConfiguration()
        {
            Periods                    = 10;
            PlayerMaxHealth            = 100;
            BaseHealthLoss             = 10;
            HealthLossPeriodModifier   = 1;
            PlayerStartingHealth       = 70;
            MaxTotalWidth              = 100;
            MaxTotalHeight             = 100;
            MaxColumnsHarvested        = 10;
            StartingHarvestSize        = 100;
            StartingHarvestValue       = 1;
            HealthRegenerationConstant = 0.01021m;
            RowGammaModifier           = 1;
            LifeEnjoymentConstant      = 464.53m;
            LifeEnjoymentAlpha         = 32;

            if (MaxColumnsHarvested > MaxTotalWidth)
            {
                MaxColumnsHarvested = MaxTotalWidth;
            }
        }
    }
}

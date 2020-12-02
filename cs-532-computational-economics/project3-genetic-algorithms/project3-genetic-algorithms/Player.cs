using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Security.Cryptography;

namespace project3_genetic_algorithms
{
    public class Player
    {
        public double MaxHealth { get; set; }
        public double CurrentHealth { get; set; }
        public int MaxRowsHarvested { get; set; }
        public List<Period> PlayPeriods { get; set; }
        public double CurrentLifeEnjoyment  { get; set; }
        public double CurrentHarvestValue { get; set; }
        public double SelectionProbability { get; set; }

        public Player()
        {
            MaxHealth            = PlayerConfiguration.PlayerMaxHealth;
            CurrentHealth        = PlayerConfiguration.PlayerStartingHealth;
            PlayPeriods          = new List<Period>();
            CurrentLifeEnjoyment = 0;
            CurrentHarvestValue  = 0;
            SelectionProbability = 0;
        }

        public Player(int currentHealth)
        {
            MaxHealth            = PlayerConfiguration.PlayerMaxHealth;
            CurrentHealth        = currentHealth;
            PlayPeriods          = new List<Period>();
            CurrentLifeEnjoyment = 0;
            CurrentHarvestValue  = 0;
            SelectionProbability = 0;
        }
        public void FindMaxRowsHarvested()
        {
            var healthEffect = (MaxHealth - CurrentHealth) / MaxHealth;
            var gammaEffect = PlayerConfiguration.RowGammaModifier * (decimal) healthEffect;
            MaxRowsHarvested = (int) Math.Floor(PlayerConfiguration.MaxTotalWidth * (1 - gammaEffect));
            if (MaxRowsHarvested > PlayerConfiguration.MaxTotalHeight)
            {
                MaxRowsHarvested = PlayerConfiguration.MaxTotalHeight;
            }
        }

        public double FindHarvestValue()
        {
            var totalArea     = Convert.ToDouble(PlayerConfiguration.MaxColumnsHarvested) * PlayerConfiguration.MaxTotalHeight;
            var harvestArea   = Convert.ToDouble(PlayerConfiguration.MaxColumnsHarvested) * MaxRowsHarvested;
            var harvestRatio  = harvestArea / totalArea;
            var harvestedDots = Math.Floor(harvestRatio * PlayerConfiguration.StartingHarvestSize);
            var harvestValue  = harvestedDots * PlayerConfiguration.StartingHarvestValue;
            return harvestValue;
        }

        public double RegenerateHealth(int healthInvestment)
        {
            var expCalc           = Math.Exp((double) (PlayerConfiguration.HealthRegenerationConstant * healthInvestment));
            var healthDelta       = (MaxHealth - CurrentHealth)/CurrentHealth;
            var denominator       = expCalc + healthDelta;
            var health            = MaxHealth * expCalc/denominator;//don't subtract current health since we are just to add it back in immediately
            var regeneratedHealth = health > MaxHealth ? MaxHealth : health;
            return regeneratedHealth;
        }

        public void UpdateCurrentHealth(int period, int healthInvestment)
        {

            CurrentHealth -= PlayerConfiguration.BaseHealthLoss - (period*PlayerConfiguration.HealthLossPeriodModifier);
            if (CurrentHealth <= 0)
            {
                CurrentHealth = 0;
                return;
            }
            var regeneratedHealth = RegenerateHealth(healthInvestment);
            CurrentHealth = Math.Floor(regeneratedHealth);
        }

        public int CalculateHealthInvestmentAmount(Period period)
        {
            var amountInvested = CurrentHarvestValue * (double) period.HealthInvestmentRatio;
            return (int) Math.Floor(amountInvested);
        }

        public int CalculateLifeInvestmentAmount(Period period)
        {
            var amountInvested = CurrentHarvestValue * (double) period.LifeInvestmentRatio;
            return (int) Math.Floor(amountInvested);
        }


        public double CalculateLifeEnjoyment(int lifeInvestment)
        {
            if (CurrentHealth == 0) return 0;

            var healthEnjoyment     = CurrentHealth / MaxHealth;
            var investmentEnjoyment = lifeInvestment / (lifeInvestment + PlayerConfiguration.LifeEnjoymentAlpha);

            var enjoyment =  PlayerConfiguration.LifeEnjoymentConstant * (decimal) healthEnjoyment * investmentEnjoyment;
            return (double) enjoyment;
        }

        public ValueTuple<decimal,decimal> GenerateLifeHealthInvestmentRatio()
        {
            var health = Convert.ToDecimal(HelperMethods.RandomNumberBetween(0.0,1.0));
            var life   = Convert.ToDecimal(HelperMethods.RandomNumberBetween(0.0,1.0));

            while (health + life > 1.0m)
            {
                health = Convert.ToDecimal(HelperMethods.RandomNumberBetween(0.0,1.0));
                life   = Convert.ToDecimal(HelperMethods.RandomNumberBetween(0.0,1.0));
            }

            return new ValueTuple<decimal, decimal>(health, life);

        }
    }
}
